import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface GameCollections {
  [key: string]: any[];
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: GameCollections;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  __type: 'Player';
}

interface MainMenuSceneData extends BaseEntity {
  __type: 'MainMenuScene';
  entities: {
    player: Player;
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: MainMenuSceneData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div 
      className="relative w-full" 
      style={{ paddingBottom: '56.25%' }}
      data-uid={props.data?.uid}
    >
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-slate-900">
        
        {/* Title Section with Image */}
        <div className="flex-1 flex items-center justify-center w-full max-w-4xl">
          <div 
            className="w-full h-48 bg-contain bg-center bg-no-repeat"
            style={{ 
              backgroundImage: 'url(/assets/title.png)',
              imageRendering: 'pixelated'
            }}
            aria-label="Game Title"
          />
        </div>

        {/* Spacer */}
        <div className="flex-1" />

        {/* Button Section */}
        <div className="flex flex-col gap-4 w-full max-w-md">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg text-xl transition-colors"
              data-uid={`${props.data?.uid}-play-button`}
            >
              <Play className="w-6 h-6" />
              Play Game
            </button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-destructive hover:bg-destructive/90 text-destructive-foreground rounded-lg text-xl transition-colors"
              data-uid={`${props.data?.uid}-quit-button`}
            >
              <XCircle className="w-6 h-6" />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
