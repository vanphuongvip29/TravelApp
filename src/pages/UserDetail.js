import { useEffect, useState } from "react"
import Apis, { endpoints } from "../configs/Apis"
import cookies from 'react-cookies';
import { Button, Table } from "react-bootstrap";
import Moment from "react-moment";


export default function UserDetail(){

    const [bill, setBill] = useState([])
    const [changed, setChanged] = useState(1)

    useEffect(()=>{
        let loadbill = async () =>{
            try{ 
                let res = await Apis.get(endpoints['getbill'], {
                    headers :{
                        "Authorization" : `Bearer ${cookies.load("access_token")}`
                    }
                })
                setBill(res.data)
                console.info(res.data)

            }catch(err){
                console.error(err)
            }
          
        }
        
        loadbill()

    },[changed])

    const load = async () => {
        try{ 
            let res = await Apis.get(endpoints['getbill'], {
                headers :{
                    "Authorization" : `Bearer ${cookies.load("access_token")}`
                }
            })
            setBill(res.data)
            console.info(res.data)

        }catch(err){
            console.error(err)
        }
      
    }
    
    const thanhToan = async (id) => {
        // id.preventDefault()
        if(window.confirm("ban co chac chan muon thanh toan ?") == true){
            try{
                let res = await Apis.post(endpoints['thanhtoan'](id), {
                    headers :{
                        "Authorization" : `Bearer ${cookies.load("access_token")}`
                    }
                })
                console.info(res.data)
                            
            }catch(err){
                  console.error(err)
            }
            alert("Thanh Toán Thành Công")
            
            load()
            console.log('BAN DA THANH TOAN' + id);
        }
        else{
            console.log('BAN CHUA THANH TOAN' + id);
        }

        
    }

    return(
        <>
        <h1 className="text-center text-danger">THONG TIN USER</h1>

        <h2>Danh Sach Cac Tour Da Dat:</h2>
        <Table striped bordered hover>
            <thead>
                <tr>
                <th>Id Tour</th>
                <th>Total price</th>
                <th>Created date</th>
                <th></th>
                </tr>
            </thead>
            
            <tbody>
            {bill.map( b =>
                <tr>
                <td>{b.book_tour}</td>
                <td>{b.total_price}</td>
                <td><Moment fromNow>{b.created_date}</Moment></td>
                {/* <td>{b.created_date}</td> */}
                <td><Button onClick={() => thanhToan(b.book_tour)} variant="info">THANH TOAN</Button></td>
                
                </tr>
            )}  
            </tbody>
            
        </Table>
    </>
    )
}