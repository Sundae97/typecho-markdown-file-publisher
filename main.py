#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path

from markdown_file_searcher import scan_files
from markdown_img_searcher import scan_imgs
from cos_pic_uploader import CosPicUploader
import config
from typecho_publisher import TypechoPublisher

uploader = CosPicUploader(
    config.secret_id,
    secret_key=config.secret_key,
    region=config.region,
    bucket=config.bucket
)

publisher = TypechoPublisher(
    config.website_xmlrpc_url,
    config.website_username,
    config.website_password
)


def execute_flow(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_base_path = os.path.dirname(file_path)
        file_base_name = os.path.splitext(os.path.basename(file_path))[0] #无后缀文件名
        md_source_text = file.read()
        md_img_urls = scan_imgs(file_path)
        if len(md_img_urls) > 0:
            for md_img_url in md_img_urls:
                img_file = os.path.join(file_base_path, md_img_url)
                img_file_name = os.path.basename(img_file)
                oss_url = uploader.upload_file(key=file_base_name+'-'+img_file_name, file_path=img_file)
                md_source_text = md_source_text.replace('](' + md_img_url + ')', '](' + oss_url + ')')
        post_id = publisher.publisher_post(file_base_name, md_source_text)
        print('发布成功 --> ' + file_base_name + ' - ' + str(post_id))


if __name__ == '__main__':
    files = scan_files(config.base_folder, config.exclude_folders)
    for md_file in files:
        execute_flow(md_file)
