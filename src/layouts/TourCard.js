import { Card, Col } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function TourCard(props){

    let path =`/tours/${props.obj.id}/imageTour`
    return(
        <Col md={4} xs={12}>
            <Card>
              <Link to={path}>
              <Card.Img variant="top" src={props.obj.image} />
              </Link>
              <Card.Body>
                <Card.Title>{props.obj.name}</Card.Title>
                <Card.Text>
                  Dia Chi: {props.obj.location}
                </Card.Text>
                <Card.Text>
                  Ngày bắt đầu: {props.obj.start_date}
                  
                </Card.Text>
                <Card.Text>
                  Ngày kết thúc: {props.obj.end_date}
                </Card.Text>
                <Card.Text>
                  Giá trẻ em: {props.obj.price_for_adults} VND
                </Card.Text>
                <Card.Text>
                  Giá người lớn: {props.obj.price_for_children} VND
                </Card.Text>
              </Card.Body>
              
              
            </Card>
          </Col>
    )
}