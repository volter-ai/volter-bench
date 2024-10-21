import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X, Settings, HelpCircle } from 'lucide-react'

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
    settings: { text: 'Settings', icon: Settings },
    help: { text: 'Help', icon: HelpCircle },
  }

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white text-center">
          {data.display_name || 'Game Title'}
        </h1>
      </div>
      
      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig]
          if (!config) return null
          
          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="flex items-center justify-center space-x-2 bg-white text-purple-600 px-8 py-3 rounded-full text-xl font-semibold hover:bg-opacity-90 transition-colors"
            >
              <config.icon className="w-6 h-6" />
              <span>{config.text}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
