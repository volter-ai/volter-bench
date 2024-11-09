import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    },
    uid: string
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <Card 
            className="w-full h-full aspect-w-16 aspect-h-9 flex flex-col items-center justify-between p-8"
            key={props.data?.uid}
        >
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold tracking-wider">
                    CREATURE GAME
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        variant="default"
                        size="lg"
                        className="w-48"
                    >
                        <Play className="mr-2 h-4 w-4" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        variant="destructive"
                        size="lg"
                        className="w-48"
                    >
                        <XCircle className="mr-2 h-4 w-4" />
                        Quit
                    </Button>
                )}
            </div>
        </Card>
    )
}
