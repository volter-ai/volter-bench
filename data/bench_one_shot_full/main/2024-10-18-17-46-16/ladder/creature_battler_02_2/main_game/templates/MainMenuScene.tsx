import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
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
    <div className="w-full h-0 pb-[56.25%] relative bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="absolute inset-0 flex flex-col justify-between items-center p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-8">
          {props.data.display_name || "Game Title"}
        </h1>

        <div className="flex flex-col items-center space-y-4 mb-8">
          {availableButtonSlugs.map((slug) => (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center justify-center px-6 py-3 bg-white text-purple-600 rounded-full font-semibold text-lg uppercase tracking-wide transition-colors duration-200 hover:bg-purple-100"
            >
              {getButtonIcon(slug)}
              {slug}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
