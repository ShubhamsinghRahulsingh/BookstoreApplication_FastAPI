from fastapi import APIRouter, Depends, status, Response
from ..utils import place_order_books, logger

routers = APIRouter(tags=["order"])


@routers.post("/place_order/", status_code=status.HTTP_201_CREATED)
def place_order(response: Response, order: dict = Depends(place_order_books)):
    try:
        if order:
            return {"message": "Order placed", "status": 201, "data": order}
        return {"message": "Order already placed", "status": 201, "data": {}}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}



