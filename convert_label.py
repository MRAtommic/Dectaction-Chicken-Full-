import os

# ระบุ Path ไปยังโฟลเดอร์ labels ของ people (ตรวจสอบ Path ให้เป๊ะนะครับ)
people_paths = [
    r'C:\Users\FEWIT\Desktop\AI Detaction\rat\train\labels',
    r'C:\Users\FEWIT\Desktop\AI Detaction\rat\valid\labels'
]

def fix_people_labels(folders):
    for folder in folders:
        if not os.path.exists(folder):
            print(f"⚠️ ไม่พบโฟลเดอร์: {folder}")
            continue
            
        count = 0
        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder, filename)
                
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    parts = line.split()
                    if len(parts) > 0:
                        # เปลี่ยนจาก 0 (ที่ AI เข้าใจว่าเป็นไก่) ให้เป็น 1 (คน)
                        parts[0] = '4' 
                        new_lines.append(" ".join(parts) + "\n")
                
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
                count += 1
        print(f"✅ แก้ไขไฟล์ใน {folder} ทั้งหมด {count} ไฟล์ เรียบร้อย!")

fix_people_labels(people_paths)