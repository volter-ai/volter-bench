import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

interface GameUIData {
    entities: {
        player: {
            uid: string
            stats: Record<string, number>
        }
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-full min-h-screen bg-gradient-to-b from-blue-900 to-blue-950">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        CREATURE BATTLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col items-center gap-6 mb-16">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center gap-3 px-8 py-4 text-xl font-semibold 
                                     bg-green-600 hover:bg-green-500 text-white rounded-lg 
                                     transition-colors duration-200"
                        >
                            <Play size={24} />
                            Play Game
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center gap-3 px-8 py-4 text-xl font-semibold 
                                     bg-red-600 hover:bg-red-500 text-white rounded-lg 
                                     transition-colors duration-200"
                        >
                            <Power size={24} />
                            Quit
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
