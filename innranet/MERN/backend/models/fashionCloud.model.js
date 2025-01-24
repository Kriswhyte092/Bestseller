import mongoose from 'mongoose';

const variantSchema = new mongoose.Schema({
  ean13: { type: Number, required: false },
  size: { type: String, required: false }, // Adjust fields as needed
  length: { type: String, required: false },
}, { _id: false });

const urlSchema = new mongoose.Schema({
  url: { type: String, required: false },
  size: { type: String, required: false },
})

const imageSchema = new mongoose.Schema({
  type: { type: String, required: false },
  url: { type: [urlSchema], required: false },
  prespective_name: { type: String, required: false },
  asset_channel: { type: String }, // Optional, for accessibility or descriptions
}, { _id: false });

const colorVariantSchema = new mongoose.Schema({
  colorName: { type: String, required: false },
  variants: { type: [variantSchema], required: false },
  images: { type: [imageSchema], required: false },
})

const productSchema = new mongoose.Schema({
  ItemNo: { type: Number, required: false },
  itemName: { type: String, required: true },
  colorVariants: {
    type: Map,
    of: colorVariantSchema,
    required: true,
  },
});

const Product = mongoose.model('Product', productSchema);


export default Product;

