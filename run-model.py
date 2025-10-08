import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def sentiment(doan_van):
    if not doan_van or not isinstance(doan_van, str):
        return "Đầu vào không hợp lệ", 0.0
    ket_qua = sentiment_pipeline(doan_van)
    nhan_cam_xuc = ket_qua[0]['label']

    return nhan_cam_xuc

if __name__ == "__main__":
    cau_tich_cuc = "This is a wonderful movie, and I highly recommend it to everyone."
    cau_tieu_cuc = "I hated this product. It broke after just one day."
    cau_tieng_viet = "Sản phẩm này rất tốt, tôi rất hài lòng."

    danh_sach_cau = [cau_tich_cuc, cau_tieu_cuc, cau_tieng_viet]
    
    for cau in danh_sach_cau:
        cam_xuc= sentiment(cau)
        print(cau +': ' + cam_xuc)

    
