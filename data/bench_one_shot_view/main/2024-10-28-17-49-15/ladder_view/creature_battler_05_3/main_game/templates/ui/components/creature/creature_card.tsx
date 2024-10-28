import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string;
  name: string;
  image: string;
  hp: number;
  maxHp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, hp, maxHp, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader className="text-center">
        <h3 className="font-semibold">{name}</h3>
      </CardHeader>
      <CardContent>
        <img src={image} alt={name} className="w-full h-40 object-contain mb-4" />
        <Progress value={(hp / maxHp) * 100} className="w-full" uid={`${uid}-progress`} />
        <p className="text-center mt-2">
          HP: {hp} / {maxHp}
        </p>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

let WrappedProgress = withClickable(Progress)

export { CreatureCard, WrappedProgress }
