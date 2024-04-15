from core.exception.order_permission_exception import OrderPermissionException


class OrderService:
    @staticmethod
    def patch_method(request, order):
        if request.user.id == order.manager_id:
            if request.data['status'] == 'new_order':
                order.manager_id = None
                order.save()
        else:
            raise OrderPermissionException
