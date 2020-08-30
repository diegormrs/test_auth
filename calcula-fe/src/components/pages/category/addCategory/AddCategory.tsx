import React, {useState} from 'react';
import {Row, Col, Typography, Input, Form, Button, message} from 'antd';
import axios from 'axios';
import {useHistory} from 'react-router';

// Translation Hook
import { setTranslations, setDefaultLanguage, useTranslation } from 'react-multi-lang';
import en from '../../../../languages/en.json';
import pt from '../../../../languages/pt.json';

setTranslations({pt, en})
setDefaultLanguage('pt')

const {Title} = Typography;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const AddCategory = () => {
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  const t = useTranslation()

  const handleSubmit = (values: any) => {
    setLoading(true);
    axios.post(`http://localhost:5000/category`, 
      values
    )
    .then(res => {
      setLoading(false);
      message.success('Category Added Successfully!');
      history.push('/category');
    })
    .catch(error => {
      setLoading(false);
      message.error(error);
    })
  }

return (
    <div>
        <Row gutter={[40, 0]}>
          <Col span={23}>
            <Title style={{textAlign: 'center'}} level={2}>
              {t('category.add.title')}
            </Title>
            </Col>
        </Row>
        <Row gutter={[40, 0]}>
        <Col span={18}>
          <Form {...layout} onFinish={handleSubmit}>
            <Form.Item name="categoryname" label={t('category.name')}
                rules={[
                {
                    required: true,
                    message: t('category.add.message.name'),
                }
                ]}
                >
              <Input placeholder={t('category.add.placeholder.name')} />
            </Form.Item>
            <div style={{textAlign: "right"}}>
                <Button type="primary" loading={loading} htmlType="submit">
                    {t('button.save')}
                </Button>{' '}
                <Button typeof="danger" htmlType="button" onClick={() => history.push('/category')}>
                    {t('button.back')}
                </Button>
            </div>
          </Form>
          </Col>
        </Row>
    </div>
  );
}

export default AddCategory;