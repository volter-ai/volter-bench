import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
  [key: string]: string;
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  __type: 'Player';
}

interface GameUIData {
  entities: {
    player: Player;
    [key: string]: BaseEntity;
  };
  uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    'play-game': { label: 'Play Game', icon: Play },
    'quit': { label: 'Quit', icon: XCircle },
  };

  return (
    <div 
      className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800"
      data-testid="main-menu-scene"
      data-uid={props.data?.uid}
    >
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
        {/* Title Section */}
        <div 
          className="flex-1 flex items-center justify-center"
          data-testid="main-menu-title-section"
        >
          <h1 
            className="text-6xl font-bold text-white tracking-wider"
            data-testid="main-menu-title"
          >
            GAME TITLE
          </h1>
        </div>

        {/* Button Section */}
        <div 
          className="flex flex-col gap-4 w-full max-w-md"
          data-testid="main-menu-buttons"
        >
          {Object.entries(buttonConfig).map(([slug, config]) => {
            if (!availableButtonSlugs?.includes(slug)) return null;

            const Icon = config.icon;
            
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center gap-2 px-8 py-4 
                         bg-slate-700 hover:bg-slate-600 
                         text-white font-semibold rounded-lg 
                         transition-colors duration-200"
                data-testid={`main-menu-button-${slug}`}
                data-uid={`${props.data?.uid}-button-${slug}`}
              >
                <Icon className="w-5 h-5" />
                <span>{config.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
