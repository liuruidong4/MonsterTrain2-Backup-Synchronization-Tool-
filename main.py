import tkinter as tk
from tkinter import messagebox, ttk
import paramiko
import os
import json
from datetime import datetime
import configparser
import time

class SaveSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MonsterTrain2存档同步工具")
        self.root.geometry("400x300")
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建GUI元素
        self.create_widgets()
        
        # 初始化SSH客户端
        self.ssh = None
        
    def load_config(self):
        """加载配置文件"""
        config = configparser.ConfigParser()
        if os.path.exists('config.ini'):
            config.read('config.ini')
        else:
            config['Server'] = {
                'hostname': '',
                'username': '',
                'password': '',
                'port': '22'
            }
            with open('config.ini', 'w') as f:
                config.write(f)
        return config
    
    def create_widgets(self):
        """创建GUI界面元素"""
        # 状态标签
        self.status_label = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # 上传按钮
        self.upload_btn = tk.Button(button_frame, text="上传存档", command=self.upload_save)
        self.upload_btn.pack(pady=10)
        
        # 下载按钮
        self.download_btn = tk.Button(button_frame, text="下载存档", command=self.download_save)
        self.download_btn.pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=20)
        
    def connect_ssh(self):
        """建立SSH连接"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=self.config['Server']['hostname'],
                username=self.config['Server']['username'],
                password=self.config['Server']['password'],
                port=int(self.config['Server']['port']),
                timeout=30
            )
            return True
        except paramiko.AuthenticationException:
            messagebox.showerror("错误", "SSH连接失败: 认证失败，请检查用户名和密码。")
            return False
        except paramiko.SSHException as e:
            messagebox.showerror("错误", f"SSH连接失败: SSH协议错误或连接问题: {str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("错误", f"SSH连接失败: 未知错误: {str(e)}")
            return False
            
    def upload_save(self):
        """上传存档文件"""
        if not self.connect_ssh():
            return
            
        try:
            local_path = os.path.expanduser("~\\AppData\\LocalLow\\Shiny Shoe\\MonsterTrain2\\metagameSave.json")
            if not os.path.exists(local_path):
                messagebox.showerror("错误", "本地存档文件不存在")
                return
                
            sftp = self.ssh.open_sftp()
            remote_path = f"/home/metagameSave.json"
            
            # 上传文件
            sftp.put(local_path, remote_path)
            messagebox.showinfo("成功", "存档上传成功")
            
        except Exception as e:
            messagebox.showerror("错误", f"上传失败: {str(e)}")
        finally:
            if self.ssh:
                self.ssh.close()
                
    def download_save(self):
        """下载存档文件"""
        if not self.connect_ssh():
            return
            
        try:
            local_path = os.path.expanduser("~\\AppData\\LocalLow\\Shiny Shoe\\MonsterTrain2\\metagameSave.json")
            remote_path = f"/home/metagameSave.json"
            
            if os.path.exists(local_path):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                backup_path = f"{os.path.splitext(local_path)[0]}_{timestamp}.json.bak"
                os.rename(local_path, backup_path)
            
            sftp = self.ssh.open_sftp()
            sftp.get(remote_path, local_path)
            messagebox.showinfo("成功", "存档下载成功")
            
        except Exception as e:
            messagebox.showerror("错误", f"下载失败: {str(e)}")
            # 如果下载失败，恢复备份
            if os.path.exists(backup_path):
                os.rename(backup_path, local_path)
        finally:
            if self.ssh:
                self.ssh.close()

    def write_log(self, action, result, detail=""):
        with open("sync.log", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{now} | {action} | {result} | {detail}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SaveSyncApp(root)
    root.mainloop()
