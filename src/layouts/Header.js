import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import cookies from 'react-cookies';
import { loginUser } from '../ActionCreators/UserCreators';
import { useLocation } from "react-router-dom";


import { useNavigate } from 'react-router-dom';




export default function Header() {

  const user = useSelector(state => state.user.user)
  const location = useLocation()
  const [kw, setKw] = useState("")
  const dispatch = useDispatch()

  const navigate = useNavigate();
  
  

  const logout = (event) => {

    event.preventDefault()

    cookies.remove("access_token")
    cookies.remove("user")
    dispatch(loginUser())
    navigate('/login')

  }

  let path =<>
    <Link className='nav-link text-danger' to="/login">Dang Nhap</Link>
    <Link className='nav-link text-danger' to="/register">Dang Ky</Link>
  </>
  if(user !== null && user != undefined){
    
    path = <>
      <Link className='nav-link text-danger' to="/user">{user.username}</Link>
      <Link className='nav-link text-danger' to="/" onClick={logout}>Dang xuat</Link>
    </>
  }
  
  const search = (event) => {
    event.preventDefault()
    navigate(`/?kw=${kw}`)
  }
  
    return (
    <>
      <Navbar bg="light" expand="lg">
        <Container fluid>
          <Navbar.Brand href="#">Travel-App</Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="me-auto my-2 my-lg-0"
              style={{ maxHeight: "100px" }}
              navbarScroll
            >
              <Link className="nav-link" to="/">HOME</Link>
              
              {path}
              
              
              
            </Nav>
            <Form className="d-flex" onSubmit={search}>
                <Form.Control
                  type="search"
                  placeholder="Search"
                  className="me-2"
                  aria-label="Search"
                  value={kw}
                  onChange={(event)=> setKw(event.target.value)}
                />
                <Button type="submit" variant="outline-success">Search</Button>
            </Form>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
}
