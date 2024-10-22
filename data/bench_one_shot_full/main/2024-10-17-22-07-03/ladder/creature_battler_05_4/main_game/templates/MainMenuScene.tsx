import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

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
        }
    }
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const {
        enabledUIDs
    } = useThingInteraction()

    const gameTitle = data.display_name || "Creature Battle"

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
            <h1 className="text-6xl font-bold text-white mt-16">{gameTitle}</h1>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full flex items-center space-x-2 transition duration-300"
                        disabled={!enabledUIDs.includes(uid)}
                    >
                        <Play size={24} />
                        <span>Play</span>
                    </button>
                )}
                
                {availableButtonSlugs.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-full flex items-center space-x-2 transition duration-300"
                        disabled={!enabledUIDs.includes(uid)}
                    >
                        <X size={24} />
                        <span>Quit</span>
                    </button>
                )}
            </div>
        </div>
    )
}
