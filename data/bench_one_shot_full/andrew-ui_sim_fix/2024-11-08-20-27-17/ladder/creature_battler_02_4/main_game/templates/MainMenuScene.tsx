import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'
import {Card} from "@/components/ui/card"
import {Button} from "@/components/ui/button"

interface GameUIData {
    entities: {
        player: {
            uid: string;
        }
    }
    uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        // 16:9 container with aspect ratio lock
        <div className="relative w-full h-0 pb-[56.25%]">
            <div className="absolute inset-0">
                {/* Main menu background */}
                <Card className="w-full h-full bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            CREATURE BATTLE
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="w-full max-w-md space-y-4">
                        {availableButtonSlugs.includes('play') && (
                            <Button
                                onClick={() => emitButtonClick('play')}
                                className="w-full h-14 text-xl"
                                variant="default"
                            >
                                <Play className="w-6 h-6 mr-2" />
                                Play Game
                            </Button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
                            <Button
                                onClick={() => emitButtonClick('quit')}
                                className="w-full h-14 text-xl"
                                variant="destructive"
                            >
                                <Power className="w-6 h-6 mr-2" />
                                Quit
                            </Button>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    )
}
