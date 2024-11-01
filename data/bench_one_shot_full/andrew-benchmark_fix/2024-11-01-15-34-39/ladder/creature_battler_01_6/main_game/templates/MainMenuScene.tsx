import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  display_name: string;
  description: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, number>;
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
  } = useCurrentButtons();

  const buttonConfig = {
    play: { label: "Play", icon: Play },
    quit: { label: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16">
        {props.data.display_name || "Main Menu"}
      </div>

      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;

          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-48 h-12 text-lg flex items-center justify-center space-x-2"
            >
              <config.icon className="w-6 h-6" />
              <span>{config.label}</span>
            </Button>
          );
        })}
      </div>

      {props.data.entities.player && (
        <div className="text-white text-sm">
          Player: {props.data.entities.player.display_name}
        </div>
      )}
    </div>
  );
}
