#找到 folder_a 和 folder_b 中具有相同文件名但扩展名不同的文件，并将它们从 folder_b 移动到 folder_c
import shutil
import os


def find_and_move_files(folder_a, folder_b, folder_c):
    if not os.path.exists(folder_c):
        os.makedirs(folder_c)
    files_a = set(os.listdir(folder_a))
    files_b = set(os.listdir(folder_b))

    file_count = 0

    common_filenames = set(os.path.splitext(filename)[0] for filename in files_a) & set(
        os.path.splitext(filename)[0] for filename in files_b)

    for common_filename in common_filenames:
        files_with_common_name_a = [filename for filename in files_a if
                                    os.path.splitext(filename)[0] == common_filename]
        files_with_common_name_b = [filename for filename in files_b if
                                    os.path.splitext(filename)[0] == common_filename]

        for file_a in files_with_common_name_a:
            for file_b in files_with_common_name_b:
                ext_a = os.path.splitext(file_a)[1]
                ext_b = os.path.splitext(file_b)[1]

                if ext_a.lower() != ext_b.lower():
                    source_file_b = os.path.join(folder_b, file_b)
                    destination = os.path.join(folder_c, file_b)
                    shutil.move(source_file_b, destination)
                    print(f"Moved {file_b} from {folder_b} to {folder_c}")
                    file_count += 1

    print(f"共移动 {file_count} 个文件")


if __name__ == "__main__":
    folder_a = r"D:\视频素材\0816\xml"           #基准文件夹
    folder_b = r"D:\视频素材\0816\new"           #需要移动的文件夹
    folder_c = r"D:\视频素材\0816\pic"           #将folder_b中的文件移动到folder_c中

    find_and_move_files(folder_a, folder_b, folder_c)
