import _beowFmt as fm
# 提早公佈營收 ####
local_file_path = f"D:/project/finlabexportdata/data/json/monthlyRevenue.json"
remote_file_path = 'static/monthlyRevenue.json'
fm.FtpFile(local_file_path, remote_file_path)

# 開收、跳空、Kbar、預估量、周轉率資料 ####
local_file_path = f"D:/project/finlabexportdata/data/json/all_info.json"
remote_file_path = 'static/all_info.json'
fm.FtpFile(local_file_path, remote_file_path)
