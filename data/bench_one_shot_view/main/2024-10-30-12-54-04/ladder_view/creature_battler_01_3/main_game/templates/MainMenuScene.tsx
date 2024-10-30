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

type ButtonSlug = 'play' | 'quit';

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButton = (slug: ButtonSlug, icon: React.ReactNode, text: string) => {
    if (availableButtonSlugs.includes(slug)) {
      return (
        <button
          key={slug}
          onClick={() => emitButtonClick(slug)}
          className="flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          {icon}
          <span className="ml-2">{text}</span>
        </button>
      );
    }
    return null;
  };

  const playerName = data?.entities?.player?.display_name || 'Player';

  return (
    <div className="w-full h-full bg-gray-800 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16">
        Game Title
      </div>
      
      <div className="text-xl text-white">
        Welcome, {playerName}!
      </div>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {renderButton('play', <Play size={24} />, 'Play')}
        {renderButton('quit', <X size={24} />, 'Quit')}
      </div>
    </div>
  );
}
