# import os
# import json
# from datetime import datetime


# def save_test_result(
#     test_name: str,
#     status: str,
#     expected_result: str,
#     actual_result: str,
#     file_name: str,
#     extra: dict | None = None
# ):
#     result_dir = os.path.join("exports", "test_results")
#     os.makedirs(result_dir, exist_ok=True)

#     result_data = {
#         "test_name": test_name,
#         "status": status,
#         "expected_result": expected_result,
#         "actual_result": actual_result,
#         "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

#     if extra:
#         result_data["extra"] = extra

#     file_path = os.path.join(result_dir, file_name)

#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(result_data, f, ensure_ascii=False, indent=4)

#     return file_path