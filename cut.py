import os
import re
import csv

def extract_functions_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    functions = []
    # 정규 표현식을 사용하여 함수 시작 부분을 찾습니다.
    patterns = [
        r"(public\s+void\s+bad\(.*?\)\s*throws\s+Throwable\s*{)",
        r"(private\s+void\s+goodG2B\(.*?\)\s*throws\s+Throwable\s*{)",
        r"(private\s+void\s+goodG2B1\(.*?\)\s*throws\s+Throwable\s*{)",
        r"(private\s+void\s+goodG2B2\(.*?\)\s*throws\s+Throwable\s*{)"
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            start_index = match.start()
            # 함수 이름 추출
            function_name = match.group().split()[1]
            # 중괄호 깊이 계산을 시작합니다.
            depth = 1
            i = match.end()
            while i < len(content) and depth > 0:
                if content[i] == '{':
                    depth += 1
                elif content[i] == '}':
                    depth -= 1
                i += 1
            # 함수 내용을 추출합니다.
            function_content = content[start_index:i]
            functions.append({
                "filename": os.path.basename(file_path),
                "function_name": function_name,
                "function_content": function_content
            })

    return functions

def process_java_files(directory_path):
    all_functions = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                full_path = os.path.join(root, file)
                functions = extract_functions_from_file(full_path)
                all_functions.extend(functions)
    
    # CSV 파일 저장
    csv_file_path = r'C:\Users\Wook\Desktop\CCIT\Data\juliet\2017-10-01-juliet-test-suite-for-java-v1-3\Java\src\testcases\CWE89_SQL_Injection\s01\Juliet_CWE89.csv'
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["filename", "function_name", "function_content"])
        writer.writeheader()
        for func in all_functions:
            writer.writerow(func)

    return csv_file_path

# 사용법 예시
directory_path = r"C:\Users\Wook\Desktop\CCIT\Data\juliet\2017-10-01-juliet-test-suite-for-java-v1-3\Java\src\testcases\CWE89_SQL_Injection\s01"  # Java 파일들이 있는 디렉토리 경로
csv_file_path = process_java_files(directory_path)
print("CSV 파일 생성 완료:", csv_file_path)
