import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
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
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-screen-lg aspect-video bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
          Creature Battle Game
        </h1>

        <div className="flex flex-col items-center mb-16">
          {availableButtonSlugs.map((slug) => (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center px-6 py-3 m-2 rounded-lg bg-white text-blue-600 hover:bg-blue-100 transition-colors"
            >
              {getButtonIcon(slug)}
              {slug.charAt(0).toUpperCase() + slug.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
