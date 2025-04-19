'use client';

import { useState } from "react";
import Head from "next/head";
import axios from "axios";
import Image from "next/image";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>([]);

  const generateRecipe = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/generate-recipe", {
        prompt,
      });
      const newRecipe = res.data.title;
      setRecipe(res.data);
      setHistory((prevHistory) => [newRecipe, ...prevHistory]);
    } catch (error) {
      console.error("Error generating recipe:", error);
      setRecipe(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Chef's Canvas</title>
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-orange-100 to-yellow-50 flex flex-col items-center p-6">
        <h1 className="text-4xl md:text-6xl font-bold text-amber-700 drop-shadow-lg mt-10">
          Chef's Canvas 🍳
        </h1>
        <p className="text-lg text-gray-600 mt-4 mb-6 max-w-xl text-center">
          Unleash your inner chef! Describe a dish, and we’ll whip up a unique recipe for you.
        </p>

        <div className="w-full max-w-2xl flex flex-col md:flex-row gap-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. A spicy vegan stew with lentils"
            className="w-full px-4 py-2 text-gray-800 placeholder-gray-500 bg-white rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400"
          />
          <button
            onClick={generateRecipe}
            disabled={loading || !prompt.trim()}
            className="bg-amber-600 hover:bg-amber-700 text-white font-semibold py-3 px-6 rounded-xl shadow-md disabled:opacity-50"
          >
            {loading ? "Cooking..." : "Generate Recipe"}
          </button>
        </div>

        {recipe && (
          <div className="bg-white rounded-2xl shadow-xl p-6 mt-10 max-w-2xl w-full border border-yellow-200">
            <h2 className="text-2xl font-bold text-amber-800 mb-2">
              🍽️ {recipe.title || "Delicious Dish"}
            </h2>
            <p className="text-gray-700 whitespace-pre-wrap">
              {recipe.recipe || "No recipe found."}
            </p>
            {recipe.image_url && (
              <div className="mt-4 w-full">
                <Image
                  src={recipe.image_url}
                  alt="Recipe"
                  width={600}
                  height={400}
                  className="rounded-xl shadow-md"
                />
              </div>
            )}
          </div>
        )}

        <div className="mt-10 w-full max-w-2xl">
          <h2 className="text-xl font-bold text-amber-700 mb-4">Recipe History</h2>
          <div className="space-y-4">
            {history.length === 0 ? (
              <p className="text-gray-600">No recipes generated yet.</p>
            ) : (
              history.map((item, index) => (
                <div
                  key={index}
                  className="p-4 bg-gray-100 rounded-xl shadow-md border border-yellow-200"
                >
                  <p className="text-lg text-gray-700">{item}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </>
  );
}
