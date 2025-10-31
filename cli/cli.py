"""
ElderlyCare CLI - 老年人关怀模型命令行工具
"""
import click
import os
import subprocess
import sys
import time
from typing import Optional

# 默认的ngrok认证令牌
DEFAULT_NGROK_TOKEN = "34SrLANwesdTMq3k60hUV9NwRfG_gKYE2sRUYhxWyhokezTP"


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """ElderlyCare - 老年人关怀模型命令行工具"""
    pass


@cli.command()
@click.option("--model-path", default="./output/elderly/sft_merged_model", help="基础模型路径或SFT合并后的模型路径")
@click.option("--adapter-path", default="./output/elderly/sft_adapter", help="LoRA适配器路径（可选）")
@click.option("--model-type", default="sft", type=click.Choice(["sft", "ppo"]), help="模型类型")
@click.option("--host", default="0.0.0.0", help="服务器监听地址")
@click.option("--port", default=8000, type=int, help="服务器端口")
@click.option("--expose", is_flag=True, help="是否通过ngrok暴露服务")
@click.option("--ngrok-token", default=None, help="ngrok认证令牌")
def start_sft(model_path, adapter_path, model_type, host, port, expose, ngrok_token):
    """启动SFT模型服务"""
    # 验证路径
    if model_path and model_path != "./output/elderly/sft_merged_model" and not os.path.exists(model_path):
        click.echo(f"❌ 错误: 模型路径不存在: {model_path}")
        return
    
    if adapter_path and adapter_path != "./output/elderly/sft_adapter" and not os.path.exists(adapter_path):
        click.echo(f"❌ 错误: 适配器路径不存在: {adapter_path}")
        return
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "api_server.elderly_api_server",
        "--model_path", model_path,
        "--model_type", model_type,
        "--host", host,
        "--port", str(port)
    ]
    
    if adapter_path:
        cmd.extend(["--adapter_path", adapter_path])
    
    click.echo("🚀 启动SFT模型服务...")
    click.echo(f"   模型路径: {model_path}")
    if adapter_path:
        click.echo(f"   适配器路径: {adapter_path}")
    click.echo(f"   模型类型: {model_type}")
    click.echo(f"   监听地址: {host}:{port}")
    
    if expose:
        # 启动ngrok
        if not start_ngrok(port, ngrok_token):
            click.echo("⚠️  ngrok启动失败，将继续启动模型服务...")
    
    # 启动模型服务
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ 启动模型服务失败: {e}")


@cli.command()
@click.option("--sft-merged-model-path", default="./output/elderly/sft_merged_model", help="SFT合并后的模型路径")
@click.option("--ppo-adapter-path", default="./output/elderly/ppo_adapter", help="PPO适配器路径")
@click.option("--host", default="0.0.0.0", help="服务器监听地址")
@click.option("--port", default=8001, type=int, help="服务器端口")
@click.option("--expose", is_flag=True, help="是否通过ngrok暴露服务")
@click.option("--ngrok-token", default=None, help="ngrok认证令牌")
def start_ppo(sft_merged_model_path, ppo_adapter_path, host, port, expose, ngrok_token):
    """启动PPO模型服务"""
    # 验证路径
    if sft_merged_model_path and sft_merged_model_path != "./output/elderly/sft_merged_model" and not os.path.exists(sft_merged_model_path):
        click.echo(f"❌ 错误: SFT合并模型路径不存在: {sft_merged_model_path}")
        return
    
    if ppo_adapter_path and ppo_adapter_path != "./output/elderly/ppo_adapter" and not os.path.exists(ppo_adapter_path):
        click.echo(f"❌ 错误: PPO适配器路径不存在: {ppo_adapter_path}")
        return
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "api_server.elderly_ppo_api_server",
        "--sft_merged_model_path", sft_merged_model_path,
        "--ppo_adapter_path", ppo_adapter_path,
        "--host", host,
        "--port", str(port)
    ]
    
    click.echo("🚀 启动PPO模型服务...")
    click.echo(f"   SFT合并模型路径: {sft_merged_model_path}")
    click.echo(f"   PPO适配器路径: {ppo_adapter_path}")
    click.echo(f"   监听地址: {host}:{port}")
    
    if expose:
        # 启动ngrok
        if not start_ngrok(port, ngrok_token):
            click.echo("⚠️  ngrok启动失败，将继续启动模型服务...")
    
    # 启动模型服务
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ 启动模型服务失败: {e}")


def start_ngrok(port: int, token: Optional[str] = None):
    """启动ngrok服务"""
    click.echo("🌐 启动ngrok服务...")
    
    # 检查ngrok是否已安装
    ngrok_path = None
    
    # 首先检查系统PATH中的ngrok
    try:
        subprocess.run(["ngrok", "--version"], check=True, capture_output=True)
        ngrok_path = "ngrok"
    except (subprocess.CalledProcessError, FileNotFoundError):
        # 检查当前目录下的ngrok
        if os.path.exists("./ngrok"):
            ngrok_path = "./ngrok"
        elif os.path.exists("./ngrok.exe"):
            ngrok_path = "./ngrok.exe"
        else:
            # 检查项目根目录下的ngrok
            project_ngrok = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ngrok")
            project_ngrok_exe = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ngrok.exe")
            if os.path.exists(project_ngrok):
                ngrok_path = project_ngrok
            elif os.path.exists(project_ngrok_exe):
                ngrok_path = project_ngrok_exe
            else:
                # 检查父目录下的ngrok（与项目目录同级）
                parent_dir = os.path.dirname(os.path.dirname(__file__))
                sibling_ngrok = os.path.join(os.path.dirname(parent_dir), "ngrok")
                sibling_ngrok_exe = os.path.join(os.path.dirname(parent_dir), "ngrok.exe")
                if os.path.exists(sibling_ngrok):
                    ngrok_path = sibling_ngrok
                elif os.path.exists(sibling_ngrok_exe):
                    ngrok_path = sibling_ngrok_exe
    
    if not ngrok_path:
        click.echo("❌ 未找到ngrok命令，请确保已安装ngrok")
        click.echo("💡 安装指南: https://ngrok.com/download")
        click.echo("💡 或者将ngrok可执行文件放在项目根目录下")
        return False
    
    click.echo(f"✅ 找到ngrok: {ngrok_path}")
    
    # 设置ngrok认证令牌
    if token:
        auth_cmd = [ngrok_path, "authtoken", token]
    else:
        auth_cmd = [ngrok_path, "authtoken", DEFAULT_NGROK_TOKEN]
    
    try:
        subprocess.run(auth_cmd, check=True, capture_output=True)
        click.echo("✅ ngrok认证完成")
    except subprocess.CalledProcessError:
        click.echo("⚠️  ngrok认证失败，尝试继续启动...")
    
    # 启动ngrok隧道
    try:
        # 在后台启动ngrok
        ngrok_process = subprocess.Popen([ngrok_path, "http", str(port)])
        click.echo(f"✅ ngrok隧道已启动，端口: {port}")
        click.echo("💡 请稍等几秒钟让ngrok获取公共URL...")
        click.echo("💡 您可以通过访问 http://localhost:4040 查看ngrok状态和公共URL")
        return True
    except Exception as e:
        click.echo(f"❌ 启动ngrok失败: {e}")
        return False


if __name__ == "__main__":
    cli()