import fetch from 'node-fetch';
import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config();


const fetchData = async (styleNumber) => {
  if (!styleNumber) {
    console.error('Stylenr ekki fundið')
    return null;
  }
  const url = `https://apigw.bestseller.com/pds/style/${styleNumber}`;
  console.log(url);

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '0d5c75bf70b244e6a7ab7480f6e39b07', // Replace with your actual token
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

const extractDataFromOptions = (options, eanToCheck) => {
  // Loop through the options
  return options.map(option => {
    const { number, colors } = option;
    const colorName = colors[0]?.name[0]?.text || [];
    const { skus, media } = option;
    const images = media?.images || []; // Get images array or default to empty
    
    const matchingSkus = skus.filter(sku => sku.ean13 === Number(eanToCheck));
    
    if (matchingSkus.length > 0) {
      return {
        number,
        colorName,
        skus: matchingSkus,
        images,
      };
    }
    return null; // Return null if no match
  }).filter(result => result !== null); // Remove null results
};
      

export const fashionCloudMain = async (styleNumber, eanToCheck) => {
  const groupedData = [];
  let dataToPush = {};
  try {
    const result = await fetchData(styleNumber); 
    for (const ean of eanToCheck) {
      if (result && result.style_variants) {
        dataToPush = {
          itemNo: result.number,
          itemName: result.name,
          colorVariants: {},
        };
        // Safeguard for result and style_variants
        result.style_variants.forEach(variant => {
          
          if (variant.options) {
            
            const data = extractDataFromOptions(variant.options, ean);
            if (data) groupedData.push(data);

          } else {
            console.log('This style variant has no options.');
          }

        });

      } else {
        console.log('Result is missing style_variants or is undefined.');
      
      }
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
  
  const colorVariants = {};
  if(groupedData.length > 0) {
    groupedData.forEach(innerArray => {
      innerArray.forEach(item => {
        if(!colorVariants[item.number]) {
          colorVariants[item.number] = {
            colorName: item.colorName,
            variants: [],
            images: fixedImages(item.images),
          };
        }
        console.log(item.skus);
        console.log(fixedImages(item.images));
        colorVariants[item.number].variants.push({
          skus: fixedSkus(item.skus),
        });
      });
    });
  }
  dataToPush.colorVariants = colorVariants; 
  return dataToPush;
  };

const fixedImages = (images) => {
  return images.map(img => {
    return {
      type: img.type,
      url: fixedUrl(img.urls),
      perspective_name: img.perspective_name,
      assetChannel: img.asset_channel_status,
    } 
  })
} 

const fixedUrl = (url) => {
  return url.map(u => {
    return {
      url: u.url,
      size: u.size,
    }
  })
}

const fixedSkus = (skus) => {
  return skus.map(sku => {
    return {
      ean13: sku.ean13,
      size: sku.size,
      length: sku.length,
    }
  })
} 
