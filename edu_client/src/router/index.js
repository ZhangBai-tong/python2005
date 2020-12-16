import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from "@/views/Home";
import Login from "@/views/Login";
import Sign_in from "@/views/Sign_in";
import Course from "@/views/Course";
import CourseDetail from "@/views/CourseDetail";
import Cart from "@/views/Cart";
import CartItem from "@/views/CartItem";
import Order from "@/views/Order";
import OrderList from "@/views/OrderList";
import OrderSuccess from "@/views/OrderSuccess";

Vue.use(VueRouter)

const routes = [
    {path: "/", redirect: "/home"},
    {path: "/home", component: Home},
    {path: "/login", component: Login},
    {path: "/sign_in", component: Sign_in},
    {path: "/course", component: Course},
    {path: "/detail/:id", component: CourseDetail},
    {path: "/cart", component: Cart},
    {path: "/cartItem", component: CartItem},
    {path: "/order", component: Order},
    {path: "/orderList", component: OrderList},
    {path: "/result", component: OrderSuccess},
]

const router = new VueRouter({
    routes,
    mode: 'history',
})

export default router
