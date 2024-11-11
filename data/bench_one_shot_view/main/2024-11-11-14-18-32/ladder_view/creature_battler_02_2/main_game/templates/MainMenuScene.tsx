import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
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
  collections: {
    creatures: BaseEntity[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    play: {
      label: "Play Game",
      icon: <Play className="w-5 h-5" />,
    },
    quit: {
      label: "Quit",
      icon: <XCircle className="w-5 h-5" />,
    }
  };

  return (
    <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8 border-0 rounded-none">
      <div className="flex-1 flex items-center justify-center flex-col gap-4">
        {/* Title Image Container */}
        <div className="w-96 h-32 bg-slate-800 rounded-lg flex items-center justify-center mb-4">
          <span className="text-slate-600">Game Title Image</span>
        </div>
      </div>

      <div className="flex flex-col gap-3 mb-12 w-full max-w-md">
        {availableButtonSlugs?.map(slug => 
          buttonConfig[slug as keyof typeof buttonConfig] && (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              variant="secondary"
              size="lg"
              className="w-full flex items-center justify-center gap-2 py-6 text-lg"
            >
              {buttonConfig[slug as keyof typeof buttonConfig].icon}
              {buttonConfig[slug as keyof typeof buttonConfig].label}
            </Button>
          )
        )}
      </div>
    </Card>
  );
}
