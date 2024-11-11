// Do not change these imports:
import {useCurrentButtons} from "@/lib/useChoices.ts";

// Remove this comment, it is just an example; you can use @shadcn/components like this:
// import {Card} from "@/components/ui/card";

import {Play, XCircle} from 'lucide-react'

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

// Note: If adding custom UI components, remember to pass UIDs as props
export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Image Section */}
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-96 h-32 bg-slate-700 flex items-center justify-center text-slate-500">
                        {/* Placeholder for game title image */}
                        <span className="text-lg">Game Title Image</span>
                    </div>
                </div>

                {/* Button Controls Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                        >
                            <Play className="w-6 h-6" />
                            <span className="text-xl">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                        >
                            <XCircle className="w-6 h-6" />
                            <span className="text-xl">Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
