import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

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
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const buttonConfig = {
    play: { label: "Play", icon: Play },
    quit: { label: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full bg-gray-800 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="w-full h-1/3 flex items-center justify-center">
        <div className="bg-gray-700 w-2/3 h-full flex items-center justify-center text-4xl font-bold text-white">
          {props.data.display_name || "Game Title"}
        </div>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;

          return (
            <Button
              key={slug}
              uid={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-48 h-12 text-lg"
              disabled={!enabledUIDs.includes(slug)}
            >
              <config.icon className="mr-2 h-5 w-5" />
              {config.label}
            </Button>
          );
        })}
      </div>
    </div>
  );
}
