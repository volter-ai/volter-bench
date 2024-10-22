import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const getButtonIcon = (slug: string) => {
    switch (slug) {
      case 'play':
        return <Play className="mr-2" />;
      case 'quit':
        return <X className="mr-2" />;
      default:
        return null;
    }
  }

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <h1 className="text-6xl font-bold text-white mt-16">Game Title</h1>
        <div className="flex flex-col items-center space-y-4 mb-16">
          {availableButtonSlugs.map((slug) => (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center justify-center w-48 px-4 py-2 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200"
            >
              {getButtonIcon(slug)}
              {slug.charAt(0).toUpperCase() + slug.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
