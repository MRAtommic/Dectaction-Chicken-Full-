from ultralytics import YOLO
import os

if __name__ == '__main__':
    # 1. ป้องกันการขัดแย้งของ Library บนระบบ Windows
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    
    # 2. โหลดโมเดลที่เทรนมาแล้ว (Fine-tuning) เพื่อเพิ่มประสิทธิภาพต่อ
    model_path = r'C:\Users\FEWIT\Desktop\AI Detaction\runs\detect\runs\detect\SuperNitro_AntiCrash_S1\weights\best.pt'
    model = YOLO(model_path) 

    # 3. เริ่มการฝึกสอนรอบสุดท้าย (Final Training Phase)
    model.train(
        data='autogen_data.yaml',      # แหล่งข้อมูลภาพและคลาส
        epochs=100,                    # จำนวนรอบในการเทรน
        imgsz=512,                     # เพิ่มขนาดภาพเป็น 512 เพื่อความคมชัดในการตรวจจับ
        batch=-1,                      # ระบบคำนวณขนาด Batch อัตโนมัติให้เต็มประสิทธิภาพ VRAM
        val=True,                      # ตรวจสอบความแม่นยำทุกรอบที่เทรน
        plots=True,                    # บันทึกกราฟแสดงผลการเทรน (Loss/mAP)
        
        # --- การตั้งค่าความเสถียรและฮาร์ดแวร์ ---
        workers=0,                     # ใช้ CPU หลักตัวเดียวเพื่อความเสถียรของแรงดันไฟ
        amp=False,                     # ปิดระบบ Mixed Precision เพื่อป้องกันไฟกระชาก
        cache=False,                   # ไม่โหลดภาพค้างใน RAM ป้องกันหน่วยความจำเต็ม
        
        # --- การปรับจูนค่าพารามิเตอร์เชิงลึก ---
        optimizer='SGD',               # ใช้ตัวปรับค่าแบบ SGD เพื่อความแม่นยำที่เสถียรในระยะยาว
        patience=20,                   # ยืดหยุ่นการหยุดเทรน (หยุดถ้าไม่เก่งขึ้นใน 20 รอบ)
        close_mosaic=20,               # ปิดระบบ Mosaic ใน 20 รอบสุดท้ายเพื่อขัดเกลาความแม่นยำ
        project='runs/detect',         # โฟลเดอร์เก็บผลงาน
        name='SuperNitro_Final_90mAP', # ชื่อรุ่นที่เน้นเป้าหมายความแม่นยำสูง
        device=0,                      # ประมวลผลผ่าน GPU (RTX 4070)
        
        # --- การสังเคราะห์ภาพเพื่อความเก่ง (Augmentation) ---
        mosaic=1.0,                    # ผสมภาพเพิ่มความฉลาด
        mixup=0.1,                     # ซ้อนภาพลดการทายผิด
        hsv_h=0.015, hsv_s=0.7,        # สุ่มปรับค่าสีและแสงของภาพ
        degrees=10.0,                  # สุ่มหมุนภาพทำมุม 10 องศา
        translate=0.1,                 # สุ่มเลื่อนวัตถุในภาพ
        scale=0.5,                     # สุ่มย่อ-ขยายวัตถุ
        fliplr=0.5                     # สุ่มพลิกภาพซ้าย-ขวา
    )