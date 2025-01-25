class Product:
    def __init__(self, name=str, itemNo=str, product_description=str, noos=False):
        self.name = name
        self.itemNo = itemNo
        self.product_description = product_description
        self.colorVariants = []
        self.noos = noos
        
    def __str__(self):
        color_variants_dict = {
            cv.colorName: [variant.size for variant in cv.variant_details] 
            for cv in self.colorVariants
        }
        return (
            f"-- Product --\n"
            f"Product Name: {self.name}\n"
            f"Item No: {self.itemNo}\n"
            f"Number of Color Variants: {len(self.colorVariants)}\n"
            f"NOOS: {self.noos}\n"
            f"Description:\n{self.product_description}"
            f"Color Variants: {color_variants_dict}\n\n"
        )

class colorVariant:
    def __init__(self, product=Product, colorName=str, colorCode=str):
        self.product = product
        self.colorName = colorName
        self.colorCode = colorCode
        self.variant_details = []
        self.image_urls = []
        
    def __str__(self):
        return (
            f"-- Color Variant --\n"
            f"Parent Product: {self.product.name} / {self.product.itemNo}\n"
            f"Color: {self.colorName}\n"
            f"Code: {self.colorCode}\n"
            f"Variants: {[v.size for v in self.variant_details]}\n"
            f"Number of images: {len(self.image_urls)}\n"
        )
    
class Variant:
    def __init__(self, colorVariant=colorVariant, BarcodeNo=int, size=str, length=str):
        self.colorVariant = colorVariant
        self.BarcodeNo = BarcodeNo
        self.size = size
        self.length = length
        
    def __str__(self):
        return (
            f"-- Variant --\n"
            f"Color Variant: {self.colorVariant.colorName}\n"
            f"Barcode: {self.BarcodeNo}\n"
            f"Size: {self.size}\n"
            f"Length: {self.length}\n"
        )
    
class Store:
    def __init__(self, store_name=str):
        self.store_name = store_name
        
    def __str__(self):
        return self.store_name
    
class Inventory:
    def __init__(self, store=Store, variant=Variant, quantity=int):
        self.store = store
        self.variant = variant
        self.quantity = quantity