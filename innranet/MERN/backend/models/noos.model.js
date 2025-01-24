import mongoose from 'mongoose';

const noosSchema = mongoose.Schema({
  ItemNo:{
  type: String,
  required: true
  },
  VariantCode:{
    type: String,
    required: false 
  },
  LocationCode:{
    type: String,
    required: true
  },
  Inventory:{
    type: Number,
    required: true
  },
  BarcodeNo:{
    type: String,
    required: false 
  },
});


const noos = mongoose.model('noos', noosSchema);

export default noos;
