import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

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
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const getButtonIcon = (slug: string) => {
    switch (slug) {
      case 'play':
        return <Play className="mr-2" />;
      case 'quit':
        return <X className="mr-2" />;
      default:
        return null;
    }
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16">
        Creature Adventure
      </div>

      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => (
          <button
            key={slug}
            onClick={() => emitButtonClick(slug)}
            className="bg-white text-purple-600 font-semibold py-3 px-6 rounded-lg shadow-lg hover:bg-purple-100 transition duration-300 flex items-center justify-center"
          >
            {getButtonIcon(slug)}
            {slug.charAt(0).toUpperCase() + slug.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}
