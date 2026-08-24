import { useState } from "react";
import { useAuthStore } from "../store/authStore";
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState("");
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    try {
      await login(formData.email, formData.password);
      navigate("/dashboard");
    } catch (error: any) {
      // console.error(error);
      setError(error.message || "Login failed. Please try again.");
    }
  };

  return (
    <div className="">
      {/* Display error message to user */}
      {error && (
        <div
          className="error-banner"
          style={{ color: "red", marginBottom: "1rem" }}
        >
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-x-5">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="email"
            required
          />
        </div>
        <div className="space-x-5">
          <label htmlFor="password">Password</label>
          <input
            type={showPass ? "text" : "password"}
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Password"
            required
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button type="submit">Login</button>
      </form>
      <p className="text-center text-slate-400 text-sm mt-6">
        New here?{" "}
        <Link
          to="/register"
          className="text-brand-400 hover:text-brand-300 font-medium"
        >
          Create account
        </Link>
      </p>
    </div>
  );
}

export default LoginPage;
