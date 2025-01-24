
import fetch from 'node-fetch';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { connectDB } from './db.js';

dotenv.config();

const validItemNos = ['10158160']; // Valid ItemNos to filter

// MongoDB Schema
const itemSchema = new mongoose.Schema({
  ItemNo: String,
  details: [
    {
      number: Number,
      colorName: String,
      skus: [
        {
          ean13: String,
          size: String,
          size_sort_order: Number,
          length: String,
        },
      ],
      barcodes: [String],
      images: [String],
    },
  ],
});

const Item = mongoose.model('Item', itemSchema);

// Fetch data from the first API
const fetchDataFromFirstAPI = async () => {
  const url = `https://bc.bestseller.is:7948/Bestseller-DEV/ODataV4/Company('VM')/variantloc?$select=ItemNo,VariantCode,LocationCode,Inventory,barcodeNo`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic S1JJU1RPRkVSOkthZmZpS2V4T2dQaXBhcjEzIQ==',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching data from first API:', error);
    return null;
  }
};

// Fetch data from the second API
const fetchDataFromSecondAPI = async (itemNo) => {
  const url = `https://apigw.bestseller.com/pds/style/${itemNo}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '0d5c75bf70b244e6a7ab7480f6e39b07',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching data from second API for ItemNo ${itemNo}:`, error);
    return null;
  }
};

// Extract and match data
const matchSkusWithBarcodes = (options, barcode) => {
  return options.map(option => {
    const { number, colors, skus, media } = option;

    const colorName = colors[0]?.name[0]?.text || [];
    const images = media?.images?.map(image => image.url)|| [];
    const barcodes = skus.map(sku => sku.ean13);
    console.log(barcodes);
    console.log(barcode);
    const matchingSkus = skus.filter(sku => {
      console.log('Checking SKU:', sku.ean13, 'against barcode:', barcode);
      // Compare both as strings (to avoid type issues)
      return sku.ean13.toString().trim() === barcode.toString().trim();
    });

    if (matchingSkus.length > 0) {
      console.log("þetta er að virka")
      // Return relevant data for matching SKUs
      return {
        number,         // Item number
        colorName,      // Color name
        skus: matchingSkus, // Matching SKUs
        barcodes,       // List of barcodes (optional, for debugging/reference)
        images: images          // Associated images
      };
    }

    return null; // Exclude options with no matching SKUs
  }).filter(result => result !== null);
};
// Save data to MongoDB
const saveToDatabase = async (data) => {
  try {
    await Item.insertMany(data);
    console.log('Data saved to MongoDB');
  } catch (error) {
    console.error('Error saving to database:', error);
  }
};

// Main function
const main = async () => {
  await connectDB();

  const firstApiData = await fetchDataFromFirstAPI();

  if (firstApiData && firstApiData.value) {
    const groupedData = {};

    // Group barcodes by ItemNo
    firstApiData.value.forEach(item => {
      if (validItemNos.includes(item.ItemNo)) {
        if (!groupedData[item.ItemNo]) {
          groupedData[item.ItemNo] = {
            ItemNo: item.ItemNo,
            barcodes: [],
          };
        }
        groupedData[item.ItemNo].barcodes.push(item.barcodeNo);
      }
    });
    let combinedData = [];

    for (const [itemNo, { barcodes }] of Object.entries(groupedData)) {
      console.log("Processing ItemNo:", itemNo);
    
      // Fetch data from second API
      const secondApiData = await fetchDataFromSecondAPI(itemNo);
      
      // Log fetched data to check if it's coming correctly
      console.log("Fetched second API data:", secondApiData);

      if (secondApiData?.style_variants) {
        secondApiData.style_variants.forEach(variant => {
          if (variant.options) {
            if (barcodes && Array.isArray(barcodes)) {  // Ensure barcodes is an array
              barcodes.forEach(barcode => {
                const matchedData = matchSkusWithBarcodes(variant.options, barcode);
            
            // Log matchedData to check if it is correct
                console.log("Matched data for barcode:", barcode, matchedData);

            // Check if matchedData is valid
                if (matchedData) {
                  // Check if ItemNo already exists in combinedData
                  const existingItem = combinedData.find(item => item.ItemNo === itemNo);
                  console.log("existingItem:", existingItem);
                  
                  if (existingItem) {
                    // If exists, push matchedData to details array
                    console.log("Adding to existing details for ItemNo:", itemNo);
                    existingItem.details.push({matchedData});
                  } else {
                    // If does not exist, create a new entry
                    console.log("Creating new entry for ItemNo:", itemNo);
                    combinedData.push({
                      ItemNo: itemNo,
                      details: matchedData,
                    });
                  }
                } else {
                  console.warn("MatchedData is empty or undefined for barcode:", barcode);
                }
              });
            } else {
          console.warn("Barcodes is not a valid array for ItemNo:", itemNo);
            }
          }
        });
      } else {
        console.warn("No style_variants found for ItemNo:", itemNo);
      }
}

    if (combinedData.length > 0) {
      await saveToDatabase(combinedData);
    } else {
      console.log('No valid data to insert.');
    }
  }

  mongoose.connection.close(() => {
    console.log('MongoDB connection closed.');
    process.exit(0);
  });
};

main();
