import { useEffect, useState } from "react";
import { Button, ButtonGroup, Form, Row } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { Link, useLocation } from "react-router-dom";
import Apis, { endpoints } from "../configs/Apis";
import TourCard from "../layouts/TourCard";
import cookies from 'react-cookies';



export default function Home() {
  
  const [tours, setTours] = useState([])
  const [prev, setPrev] = useState(false)
  const [next, setNext] = useState(false)
  const [page, setPage] = useState(1)
  const location = useLocation()
  const [kw, setKw] = useState("")
  // const dispatch = useDispatch()



  useEffect(() => {
    let loadTours = async () => {
        let query = location.search
        if (query === "")
          query = `?page=${page}`
        else
          query += `&page=${page}`

        try{
          let res = await Apis.get(`${endpoints['tours']}${query}`)
          setTours(res.data.results)

          setNext(res.data.next != null)
          setPrev(res.data.previous !== null)
          console.info(res.data)
        } catch(err){
          console.error(err)
        }

        
      }

      loadTours()
  }, [location.search, page])

  const paging = (inc) =>{
    setPage(page + inc)
  }





  return (
    <>
      <h1 className="text-center text-danger">DANH SACH TOURS</h1>
      
      <ButtonGroup>
        <Button variant="info" onClick={()=> paging(-1)} disabled={!prev}>&lt;&lt;</Button>
        <Button variant="info" onClick={()=> paging(1)} disabled={!next}>&gt;&gt;</Button>

        
        
        
        
      </ButtonGroup>
      <hr></hr>
      
      <Row>
          {tours.map(t => <TourCard obj={t} />)}
      </Row>
    </>
  );
}
