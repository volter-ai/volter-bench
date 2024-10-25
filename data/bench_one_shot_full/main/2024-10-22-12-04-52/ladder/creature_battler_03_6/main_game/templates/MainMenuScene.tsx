import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

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

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  }

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8 text-white">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mt-16">
          {data.display_name || "Creature Battle"}
        </h1>
        
        <div className="flex flex-col items-center space-y-4 mb-16">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig]
            if (!config) return null
            
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="bg-white text-blue-600 font-semibold py-2 px-6 rounded-full flex items-center space-x-2 hover:bg-blue-100 transition-colors"
              >
                <config.icon size={24} />
                <span>{config.text}</span>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
