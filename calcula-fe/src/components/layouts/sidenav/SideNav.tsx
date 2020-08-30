import React from 'react';
import './SideNav.css';
import { Menu } from 'antd';
import { UserOutlined, UploadOutlined } from '@ant-design/icons';

import {useHistory}  from 'react-router';

// Translation Hook
import { setTranslations, setDefaultLanguage, useTranslation } from 'react-multi-lang';
import en from '../../../languages/en.json';
import pt from '../../../languages/pt.json';

setTranslations({pt, en})
setDefaultLanguage('pt')


const SideNav = () => { const history = useHistory();

  const t = useTranslation()

  const handleCategoryClick = () => {
    history.push('/category');
  }

  const handleStockClick = () => {
    history.push('/stock');
  }

  const handleProductClick = () => {
    history.push('/product');
  }


  return (
    <div>
        <div style={{height: "32px", background: "rgba(255, 255, 255, 0.2)", margin: "16px"}}></div>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1" onClick={handleCategoryClick}>
                <UploadOutlined />
                <span> {t('category.title')} </span>
            </Menu.Item>
            <Menu.Item key="2" onClick={handleProductClick}>
                <UserOutlined />
                <span> {t('products.title')} </span>
            </Menu.Item>
            <Menu.Item key="3" onClick={handleStockClick}>
                <UploadOutlined />
                <span> {t('stock.title')} </span>
            </Menu.Item>
        </Menu>
    </div>
  );
  
}

export default SideNav;