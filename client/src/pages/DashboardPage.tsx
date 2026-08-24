import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  BookOpen,
  ChevronRight,
  Flame,
  Star,
  Trophy,
  Loader2,
  Sparkles,
  Lock,
  CheckCircle2,
  Clock,
  RefreshCw,
} from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { api } from "../lib/api";
import type { Lesson, Stats } from "@/types";
import {
  getLevelLabel,
  getLevelColor,
  getStatusColor,
  getStatusLabel,
  xpToLevel,
} from "../lib/utils";

export default function DashboardPage() {
  const { user, refreshUser } = useAuthStore();
  const [stats, setStats] = useState<Stats | null>(null);
  const navigate = useNavigate();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [activeLevel, setActiveLevel] = useState(1);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [lessonsRes, stateRes] = await Promise.all([
        api.GET("/api/lessons"),
        api.GET("/api/progress/stats"),
      ]);
      if (lessonsRes.data) setLessons(lessonsRes.data as Lesson[]);
      if (stateRes.data) setStats(stateRes.data as Stats);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);
  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSeed = async () => {
    try {
      setSeeding(true);
      await api.POST("/api/lessons/seed");
      await loadData();
      await refreshUser();
    } catch (error) {
      console.error(error);
    } finally {
      setSeeding(false);
    }

    const {
      level: userLevel,
      progress: xpProgress,
      nextLevelXp,
    } = xpToLevel(user?.total_xp || 0);
    const leveledLessons = lessons.filter((l) => l.level === activeLevel);

    const levels = [...new Set(lessons.map((l) => l.level))].sort(
      (a, b) => a - b,
    );

    // const levels = [...new Set(lessons.map((l) => l.level))].sort();

    const isLessonUnlocked = (lesson: Lesson, idx: number) => {
      if (idx === 0) return true;
      const prev = leveledLessons[idx - 1];
      return prev?.status === "completed" || prev?.status === "mastered";
    };

    if (loading) {
      return (
        <div className="flex items-center justify-center min-h-64">
          <Loader2 className="w-8 h-8 text-brand-400 animate-spin" />
        </div>
      );
    }
  };

  return (
    <div>
      <div>
        <h1 className="text-2xl font-display font-bold text-gray-500">
          Hello, {user?.name?.split(" ")[0]}! 👋
        </h1>
        <p className="text-slate-700 mt-1 text-sm">
          {stats?.completed_lessons
            ? `${stats.completed_lessons} lessons completed — keep going!`
            : "Your learning journey starts here."}
        </p>

        <button
          onClick={() => navigate("/daily-review")}
          className="flex items-center gap-2 btn-secondary text-sm py-2 px-4 whitespace-nowrap"
        >
          <RefreshCw className="w-4 h-4" />
          <span className="hidden sm:inline">Daily Review</span>
        </button>
      </div>

      {/* Stats row */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            {
              icon: Flame,
              label: "Streak",
              value: `${user?.current_streak || 0}d`,
              color: "text-saffron-400",
              bg: "bg-saffron-400/10",
            },
            {
              icon: Star,
              label: "Total XP",
              value: user?.total_xp?.toLocaleString() || "0",
              color: "text-brand-400",
              bg: "bg-brand-400/10",
            },
            {
              icon: CheckCircle2,
              label: "Completed",
              value: `${stats.completed_lessons}/${stats.total_lessons}`,
              color: "text-emerald-400",
              bg: "bg-emerald-400/10",
            },
            {
              icon: Trophy,
              label: "Avg Score",
              value: `${stats.avg_score}%`,
              color: "text-purple-400",
              bg: "bg-purple-400/10",
            },
          ].map(({ icon: Icon, label, value, color, bg }) => (
            <div key={label} className="card p-4">
              <div
                className={`w-8 h-8 rounded-lg ${bg} flex items-center justify-center mb-2`}
              >
                <Icon className={`w-4 h-4 ${color}`} />
              </div>
              <div className="text-slate-600 font-display font-bold text-lg leading-none">
                {value}
              </div>
              <div className="text-slate-500 text-xs mt-1">{label}</div>
            </div>
          ))}
        </div>
      )}

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-display font-semibold text-black">
            Lessons
          </h2>
          {lessons.length === 0 && (
            <button
              onClick={handleSeed}
              disabled={seeding}
              className="flex items-center gap-2 btn-saffron text-sm py-2 px-4"
            >
              {seeding ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Sparkles className="w-4 h-4" />
              )}
              {seeding ? "Generating..." : "Generate Lessons"}
            </button>
          )}
        </div>
        {lessons.length === 0 ? (
          <div>
            <p className="text-slate-300 font-semibold mb-2">No lessons yet</p>
          </div>
        ) : (
          <>
            {levels.length > 1 && (
              <div className="flex gap-2 mb-4">
                {levels.map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setActiveLevel(lvl)}
                    className={`px-4 py-1.5 rounded-lg text-sm font-semibold transition-all duration-200
                      ${activeLevel === lvl ? "bg-brand-500 text-white" : "bg-white/5 text-slate-400 hover:text-white"}`}
                  >
                    {getLevelLabel(lvl)}
                  </button>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
