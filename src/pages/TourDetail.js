import { useEffect, useState } from "react"
import { Button, Card, Col, Form, Image, Row } from "react-bootstrap"
import Moment from "react-moment"
import { useSelector } from "react-redux"
import { Link, useNavigate, useParams } from "react-router-dom"
import Apis, { endpoints } from "../configs/Apis"
import TourCard from "../layouts/TourCard"
import cookies from 'react-cookies';
import Rating from "react-rating"


export default function TourDetail(){

    const [image, setImages] = useState([])
    const [comments, setComments] = useState([])
    const [commentContent, setCommentContent] = useState(null)
    const [rate, setRate] = useState(0)
    const [changed, setChanged] = useState(1)
    const { tourId } = useParams()
    let user = useSelector(state => state.user.user)
    const [adult, setAdult] = useState()
    const [children, setChildren] = useState()
    const [rating, setRating] = useState([])

    const navigate = useNavigate()

    useEffect(()=>{
        let loadImage = async () =>{
            try{ 
                let res = await Apis.get(endpoints['imageTours'](tourId))
                setImages(res.data)
                console.info(res.data)

            }catch(err){
                console.error(err)
            }
          
        }
        let loadComments = async () =>{
            try{
                let res = await Apis.get(endpoints['comments'](tourId))
                setComments(res.data)
            }catch(err){
                console.error(err)
            }
        }

        let loadRate = async () => {
            try{
                let res = await Apis.get(endpoints['getrate'](tourId))
                setRating(res.data)

            }
            catch(err){
                console.error(err)
            }
        }

        loadImage()
        loadComments()
        loadRate()

    },[changed])

    const addComment = async (event) => {
        event.preventDefault()
        try{
            let res = await Apis.post(endpoints['add-comment'](tourId),{
                "content" : commentContent
            }, {
                headers :{
                    "Authorization" : `Bearer ${cookies.load("access_token")}`
                }
            })
            console.info(res.data)
            comments.push(res.data)
            setComments(comments)
            setChanged(comments.length)
        }catch(err){
            console.error(err)
        }

    }
    const saveRating = async(rate) =>{
        if(window.confirm("ban muon danh gia ?") == true){
            try{
                let res = await Apis.post(endpoints['rating'](tourId),{
                    "rating": rate
                },{
                    headers :{
                        "Authorization" : `Bearer ${cookies.load("access_token")}`
                    }
                })

                console.info(res.data)
            }catch(err){
                console.error(err)
            }
        }

    }
    
    let comment = <em><Link to="/login">DANG NHAP</Link> DE BINH LUAN</em>
    let r =""
    if(user != null && user !== undefined){
        comment = <Form onSubmit={addComment}>         
                        <Form.Group className="mb-3" controlId="commnetContent">                           
                            <Form.Control as="textarea"
                                            value={commentContent} 
                                            onChange={(event)=> setCommentContent(event.target.value)}
                                            placeholder="Nhap Binh Luan" rows={3} />
                        </Form.Group>
                        <Button type="submit" variant="info">Them binh luan</Button>
                    </Form>

        r = <Rating initialRating={rate} onClick={saveRating}/>
    }
    


    const booktour = async (event) => {
        event.preventDefault()
        if(window.confirm("ban co muon dat tour ?") == true){
            try{
                let res = await Apis.post(endpoints['booktour'],{
                    "num_of_adults": adult,
                    "num_of_children": children,
                    "tour" : tourId,
                    "user" : user.id
                }, {
                    headers :{
                        "Authorization" : `Bearer ${cookies.load("access_token")}`
                    }
                })
                console.info(res.data)
                alert("Đã đặt tour thành công")
            }catch(err){
                console.error(err)
            }
        }

        navigate('/user')


    }
    let book =""
    if(user != null && user !== undefined){
        book =  <Form onSubmit={booktour}>
        <Form.Group className="mb-3" controlId="num_of_adult">
            <Form.Label>num_of_adult</Form.Label>
            <Form.Control type="number"
                value={adult}
                onChange={(event)=> setAdult(event.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="num_of_children">
            <Form.Label>num_of_children</Form.Label>
            <Form.Control type="number" 
                value={children}
                onChange={(event)=> setChildren(event.target.value)}/>
        </Form.Group>
        <Button type="submit" variant="info">Dat Tour</Button>
    </Form>
    }

    return(
        <>
        <h1 className="text-center text-danger">CHI TIET TOUR</h1>
        <Row>
        {image.map(i=>
            
                <Col md={4} xs={12}>
                
                    <Card>
                    
                    <Card.Img variant="top" src={i.image} />
                    
                    <Card.Body>
                        <Card.Text>
                        Description: {i.descriptions}
                        </Card.Text>
                    </Card.Body>
                    </Card>
                    {/* <h4>Danh gia tour:</h4> */}
                                            {r}
                </Col>
                
            
          )}
        </Row>

        <h4>Các Đánh Giá</h4>
        <Row>
            {rating.map(r=> <Rating
                                
                                initialRating={r.star_rate}
                                readonly
                                />)}
            
            
        </Row>
        {/* <Form onSubmit={booktour}>
            <Form.Group className="mb-3" controlId="num_of_adult">
                <Form.Label>num_of_adult</Form.Label>
                <Form.Control type="number"
                    value={adult}
                    onChange={(event)=> setAdult(event.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="num_of_children">
                <Form.Label>num_of_children</Form.Label>
                <Form.Control type="number" 
                    value={children}
                    onChange={(event)=> setChildren(event.target.value)}/>
            </Form.Group>
            <Button type="submit" variant="info">Dat Tour</Button>
        </Form> */}
        {book}
        
        <hr/>
        {comment}
        <hr/>
        {comments.map(c => <Row>
                                <Col md={1} xs={3}>
                                    <Image src={c.user.avatar} roundedCircle fluid></Image>
                                    <p>{c.user.username} </p>
                                </Col>
                                <Col md={11} xs={9}>
                                    <p><em>{c.content}</em></p>
                                    <p>Da binh luan: <Moment fromNow>{c.created_date}</Moment></p>
                                </Col>
                            </Row> )}
        
        </>
    )
}