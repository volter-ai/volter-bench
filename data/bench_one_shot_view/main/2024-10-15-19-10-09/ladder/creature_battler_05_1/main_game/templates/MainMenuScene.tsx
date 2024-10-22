import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any>;
      display_name: string;
      description: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const buttonConfig = {
    play: { label: "Play", icon: Play },
    quit: { label: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9', background: 'linear-gradient(to bottom, #3b82f6, #8b5cf6)' }}>
      <div className="w-full max-w-2xl h-1/3 flex items-center justify-center" style={{ background: '#d1d5db', borderRadius: '0.5rem' }}>
        <h1 className="text-4xl font-bold" style={{ color: '#1f2937' }}>Game Title</h1>
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
              className="w-48 h-12 text-lg flex items-center justify-center"
              style={{ opacity: enabledUIDs.includes(slug) ? 1 : 0.5, pointerEvents: enabledUIDs.includes(slug) ? 'auto' : 'none' }}
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
