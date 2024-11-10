import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameStats {
    [key: string]: number | undefined;
}

interface GameMeta {
    prototype_id?: string;
    category?: string;
    [key: string]: string | undefined;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name?: string;
    description?: string;
}

interface Player extends BaseEntity {
    __type: 'Player';
}

interface GameUIData {
    entities: {
        player?: Player;
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data) {
        return <div className="w-full h-full flex items-center justify-center">
            <p className="text-muted-foreground">Loading...</p>
        </div>
    }

    return (
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <Card className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800 rounded-none border-0">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-primary tracking-wider">
                        GAME TITLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.length === 0 ? (
                        <p className="text-center text-muted-foreground">No actions available</p>
                    ) : (
                        <>
                            {availableButtonSlugs.includes('play') && (
                                <Button
                                    variant="default"
                                    size="lg"
                                    onClick={() => emitButtonClick('play')}
                                    className="w-full text-xl py-6"
                                >
                                    <Play className="w-6 h-6 mr-2" />
                                    Play Game
                                </Button>
                            )}

                            {availableButtonSlugs.includes('quit') && (
                                <Button
                                    variant="destructive"
                                    size="lg"
                                    onClick={() => emitButtonClick('quit')}
                                    className="w-full text-xl py-6"
                                >
                                    <XCircle className="w-6 h-6 mr-2" />
                                    Quit
                                </Button>
                            )}
                        </>
                    )}
                </div>
            </Card>
        </div>
    );
}
