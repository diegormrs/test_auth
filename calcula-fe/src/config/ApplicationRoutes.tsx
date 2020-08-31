import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import List from "../components/pages/list/List";
import Home from "../components/pages/home/Home";
import Form from "../components/pages/form/Form";
import SideNav from "../components/layouts/sidenav/SideNav";
import Category from "../components/pages/category/Category";
import AddCategory from '../components/pages/category/addCategory/AddCategory'
import Stock from "../components/pages/stock/Stock";
import Product from "../components/pages/product/Product";
import AddProduct from "../components/pages/product/addProduct/AddProduct";
import EmptyPage from "../components/pages/empty/Empty";
import { Layout } from 'antd';

import { MenuUnfoldOutlined, MenuFoldOutlined } from '@ant-design/icons';

const { Header, Sider, Content} = Layout;

const ApplicationRoutes = () => {
  const [collapse, setCollapse] = useState(false);

  useEffect(() => {
    window.innerWidth <= 760 ? setCollapse(true) : setCollapse(false);
  }, []);

  const handleToggle = (event: any) => {
        event.preventDefault();
        collapse ? setCollapse(false) : setCollapse(true);
  }

  return (
    <Router>
      <Layout>
        <Sider trigger={null} collapsible collapsed={collapse}>
          <SideNav />
        </Sider>
        <Layout>
          <Header className="siteLayoutBackground" style={{padding: 0, background: "#001529"}}>
                    {React.createElement(collapse ? MenuUnfoldOutlined : MenuFoldOutlined, {
                        className: 'trigger',
                        onClick: handleToggle,
                        style: {color: "#fff"}
                    })}
          </Header>
            <Content style={{margin: '24px 16px', padding: 24, minHeight: "calc(100vh - 114px)", background: "#fff"}}>
              <Switch>
                  <Route path="/list" component={List} />
                  <Route path="/home" component={Home} />
                  <Route path="/category" component={Category} />
                  <Route path="/addCategory" component={AddCategory} />
                  <Route path="/product" component={Product} />
                  <Route path="/addProduct" component={AddProduct} />
                  <Route path="/stock" component={Stock} />
                  <Route path="/form" component={Form} />
                  <Route path="/empty" component={EmptyPage} />
                  <Redirect to="/home" from="/" />
              </Switch>
            </Content>
        </Layout>
      </Layout>
  </Router>
  );
}
export default ApplicationRoutes;