import { useState } from "react";
import API from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("token") ? true : false
  );
  const [userRole, setUserRole] = useState(localStorage.getItem("role") || "");
  const [orders, setOrders] = useState([]);

  const [customerName, setCustomerName] = useState("");
  const [itemName, setItemName] = useState("");
  const [quantity, setQuantity] = useState("");

  const login = async (e) => {
    e.preventDefault();

    try {
      const response = await API.post("/auth/login", {
        email: email,
        password: password,
      });

      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("role", response.data.role);

      setIsLoggedIn(true);
      setUserRole(response.data.role);

      alert("Login successful");
      fetchOrders();
    } catch (error) {
      alert("Login failed");
      console.log(error.response?.data || error);
    }
  };

  const register = async (e) => {
    e.preventDefault();

    try {
      await API.post("/auth/register", {
        email: email,
        password: password,
      });

      alert("Registration successful. Now login.");
    } catch (error) {
      alert("Registration failed");
      console.log(error.response?.data || error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await API.get("/orders");
      setOrders(response.data);
    } catch (error) {
      alert("Failed to fetch orders");
      console.log(error.response?.data || error);
    }
  };

  const createOrder = async (e) => {
    e.preventDefault();

    try {
      await API.post("/orders", {
        customer_name: customerName,
        item_name: itemName,
        quantity: Number(quantity),
      });

      alert("Order created successfully");

      setCustomerName("");
      setItemName("");
      setQuantity("");

      fetchOrders();
    } catch (error) {
      alert("Failed to create order");
      console.log(error.response?.data || error);
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await API.patch(`/orders/${orderId}`, {
        status: newStatus,
      });

      alert("Order status updated");
      fetchOrders();
    } catch (error) {
      alert("Failed to update order status");
      console.log(error.response?.status);
      console.log(error.response?.data);
    }
  };

  const getNextStatus = (currentStatus) => {
    if (currentStatus === "PENDING") {
      return "PROCESSING";
    }

    if (currentStatus === "PROCESSING") {
      return "SHIPPED";
    }

    if (currentStatus === "SHIPPED") {
      return "DELIVERED";
    }

    return null;
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    setIsLoggedIn(false);
    setUserRole("");
    setOrders([]);
  };

  return (
    <div>
      <h1>Order Management Dashboard</h1>

      {!isLoggedIn ? (
        <div>
          <h2>Login / Register</h2>

          <form>
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button type="button" onClick={login}>
              Login
            </button>

            <button type="button" onClick={register}>
              Register
            </button>
          </form>
        </div>
      ) : (
        <div>
          <button onClick={logout}>Logout</button>

          <h2>Create Order</h2>

          <form onSubmit={createOrder}>
            <input
              type="text"
              placeholder="Customer name"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
            />

            <input
              type="text"
              placeholder="Item name"
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
            />

            <input
              type="number"
              placeholder="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />

            <button type="submit">Create Order</button>
          </form>

          <h2>Orders</h2>

          <button onClick={fetchOrders}>Refresh Orders</button>

          <table border="1">
            <thead>
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Item</th>
                <th>Quantity</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {orders.map((order) => {
                const nextStatus = getNextStatus(order.status);

                return (
                  <tr key={order.id}>
                    <td>{order.id}</td>
                    <td>{order.customer_name}</td>
                    <td>{order.item_name}</td>
                    <td>{order.quantity}</td>
                    <td>{order.status}</td>
                    <td>
                      {userRole === "ADMIN" ? (
                        nextStatus ? (
                          <button
                            onClick={() =>
                              updateOrderStatus(order.id, nextStatus)
                            }
                          >
                            Mark as {nextStatus}
                          </button>
                        ) : (
                          <span>Completed</span>
                        )
                      ) : (
                        <span>View only</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;