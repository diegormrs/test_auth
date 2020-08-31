import React, {useEffect, useState} from 'react';
import {Table, Row, Col, Button, Typography} from 'antd';
import {useHistory} from 'react-router';
import axios from 'axios';

// Translation Hook
import { setTranslations, setDefaultLanguage, useTranslation } from 'react-multi-lang';
import en from '../../../languages/en.json';
import pt from '../../../languages/pt.json';

setTranslations({pt, en})
setDefaultLanguage('pt')

const {Title} = Typography;

const Category = () => { 
    const history = useHistory();
    const [allData, setAllData] = useState([]);

    const t = useTranslation()

    useEffect(() => {
        axios.get(`http://localhost:5000/category`).then(res => {
        setAllData(res.data);
        });
    },[]);

    const columns = [
      {
        title: t('category.name'),
        dataIndex: 'categoryname',
      }
    ];

    const data = [{}];

    allData.map((category: any) => {
        data.push({
        key: category.id,
        categoryname: category.categoryname
      })
      return data;
    });

    const handleClick = () => {
        history.push('/addCategory')
    }

  return (
    <div>
        <Row gutter={[40, 0]}>
          <Col span={18}>
            <Title level={2}>
              {t('category.title')}
            </Title>
            </Col>
          <Col span={6}>
          <Button onClick={handleClick} block>Add Category</Button>
          </Col>
        </Row>
        <Row gutter={[40, 0]}>
        <Col span={24}>
        <Table columns={columns} dataSource={data} />
        </Col>
        </Row>
    </div>
  );
}

export default Category;