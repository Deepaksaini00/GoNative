import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

function RegisterPage() {
  const [formData, setformData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState("");
  const { register, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setformData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    try {
      await register(formData.name, formData.email, formData.password);
      navigate("/dashboard");
    } catch (error: any) {
      // console.error(error);
      setError(error.message || "Network error. Please try again.");
    }
  };

  return (
    <div className="">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-x-5">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your name"
            required
          />
        </div>
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

        <div className="bg-white/3 border border-white/6 rounded-xl p-3 text-sm text-slate-400">
          <span className="text-saffron-400 font-medium">Learning path:</span>{" "}
          <span className="font-hindi">हिंदी</span> → English
        </div>

        {error && <p className="text-red-500">{error}</p>}
        <button type="submit">Register</button>
      </form>

      <p className="text-center text-slate-400 text-sm mt-6">
        Already have an account?{" "}
        <Link
          to="/login"
          className="text-brand-400 hover:text-brand-300 font-medium"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}

export default RegisterPage;
