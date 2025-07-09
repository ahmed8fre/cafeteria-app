import ast

user_input_string = "[1,2],[3,4]"

try:
    # نقوم بإضافة أقواس مربعة خارجية لجعلها قائمة من القوائم
    # لأن "[1,2],[3,4]" هو تعبير عن عناصر متعددة، وليس قائمة واحدة
    # لكي يتم تقييمها كقائمة واحدة، يجب أن تكون محاطة بأقواس مربعة
    formatted_string = f"[{user_input_string}]" # ستصبح "[ [1,2],[3,4] ]"
    
    # تحويل السلسلة النصية إلى قائمة بايثون حقيقية
    result_list = ast.literal_eval(formatted_string)
    
    print(f"السلسلة النصية المدخلة: {user_input_string}")
    print(f"السلسلة النصية المهيأة: {formatted_string}")
    print(f"القائمة الناتجة: {result_list}")
    print(f"نوع القائمة الناتجة: {type(result_list)}")
    print(f"نوع العنصر الأول في القائمة: {type(result_list[0])}")

except (ValueError, SyntaxError) as e:
    print(f"حدث خطأ في تحويل الإدخال: {e}")
    print("الرجاء التأكد من أن الإدخال بصيغة صحيحة مثل: [1,2],[3,4]")

# مثال آخر لإدخال سليم من المستخدم مباشرة كقائمة
user_input_string_correct = "[[5,6],[7,8]]"
try:
    result_list_correct = ast.literal_eval(user_input_string_correct)
    print(f"\nالسلسلة النصية المدخلة الصحيحة: {user_input_string_correct}")
    print(f"القائمة الناتجة الصحيحة: {result_list_correct}")
except (ValueError, SyntaxError) as e:
    print(f"حدث خطأ في تحويل الإدخال: {e}")