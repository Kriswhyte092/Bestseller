import fetch from 'node-fetch';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { connectDB } from './db.js';
import { fashionCloudMain } from './fashionCloudAPI.js';
import Product from '../models/fashionCloud.model.js';
dotenv.config();

const validItemNos = ['10148253']; // Valid ItemNos to filter

const fetchData = async () => {
  const url = `https://bc.bestseller.is:7948/Bestseller-DEV/ODataV4/Company('VM')/variantloc?$select=ItemNo,VariantCode,LocationCode,Inventory,barcodeNo`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic S1JJU1RPRkVSOkthZmZpS2V4T2dQaXBhcjEzIQ==',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

// Schema for the Variant (with the assumption that the ItemNo should be unique and variants are an array)
const variantSchema = new mongoose.Schema({
  ItemNo: Number,
  variants: [
    {
      VariantCode: String,
      LocationCode: String,
      Inventory: Number,
      barcodeNo: String,
    }
  ],
});

const Variant = mongoose.model('Variant', variantSchema);

// Function to save data to MongoDB
const saveToDatabase = async (data) => {
  try {
    await Variant.insertMany(data);
    console.log('Data saved to MongoDB');
  } catch (error) {
    console.error('Error saving to database:', error);
  }
};

const fashionCloudToDatabase = async (data) => {
 
  try {
    const document = {
      itemNo: data.itemNo,
      itemName: data.itemName,
      colorVariants: [],
    };
      
    Object.entries(data.colorVariants).forEach(([key, colorVariant]) => {
        
        const colorVariantData = {
          colorName: colorVariant.colorName,
          variants: colorVariant.variants,
          images: colorVariant.images
        };

        // Add the color variant data to the document
        document.colorVariants.push(colorVariantData);
    });

    await Product.create(data);
    console.log('data saved to MongoDB for fashioncloud');
  } catch (error){
    console.error("helvitis fokking fokk", error);
  } 
};
// Main function to control the flow
const main = async () => {
  await connectDB();
  const data = await fetchData();

  if (data && data.value) {
    // Grouping variants by ItemNo
    const groupedData = {};

    // Filter and group data
    data.value.forEach(item => {
      if (validItemNos.includes(item.ItemNo)) {
        if (!groupedData[item.ItemNo]) {
          groupedData[item.ItemNo] = {
            ItemNo: item.ItemNo,
            variants: [],
          };
        }

        // Add the variant details to the respective ItemNo group
        groupedData[item.ItemNo].variants.push({
          VariantCode: item.VariantCode,
          LocationCode: item.LocationCode,
          Inventory: item.Inventory,
          barcodeNo: item.barcodeNo,
        });
      }
    });

    // Convert groupedData object to an array to insert into MongoDB
    const dataToInsert = Object.values(groupedData);
    const getVariantData = [];
    for (const item of dataToInsert) {
      for (const variant of item.variants) {
        getVariantData.push(variant.barcodeNo);
      }
      console.log(item.ItemNo, getVariantData);
      try {
        const fashionCloudData = await fashionCloudMain(item.ItemNo, getVariantData);
        console.log(fashionCloudData);
        if (fashionCloudData) {
          await fashionCloudToDatabase(fashionCloudData);
        }
      } catch (error) {
        console.error('error sjuddan fokker');
      }
    }


    if (dataToInsert.length > 0) {
      await saveToDatabase(dataToInsert);
    } else {
      console.log('No valid data to insert.');
    }
  
  }

  
  // Close the MongoDB connection and exit the script
  mongoose.connection.close(() => {
    console.log('MongoDB connection closed.');
    process.exit(0); // Exit the script
  });
};

main();
