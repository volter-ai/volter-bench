import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'
import {Button} from "@/components/ui/button"

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

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div 
            uid="main-menu-container"
            className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800"
        >
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Image Section */}
                <div 
                    uid="title-section"
                    className="flex-1 flex items-center justify-center"
                >
                    <div 
                        uid="title-image"
                        className="w-96 h-32 bg-slate-700 flex items-center justify-center text-slate-500"
                        aria-label="Game Title Image"
                    >
                        [Title Image Placeholder]
                    </div>
                </div>

                {/* Button Section */}
                <div 
                    uid="button-container"
                    className="flex flex-col gap-4 w-full max-w-md"
                >
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            uid="play-button"
                            onClick={() => emitButtonClick('play')}
                            className="w-full py-6 text-xl"
                            variant="default"
                        >
                            <Play className="w-6 h-6 mr-2" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            uid="quit-button"
                            onClick={() => emitButtonClick('quit')}
                            className="w-full py-6 text-xl"
                            variant="destructive"
                        >
                            <XCircle className="w-6 h-6 mr-2" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
