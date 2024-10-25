import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"

interface CreatureCardProps extends React.ComponentPropsWithoutRef<typeof Card> {
  uid: string;
  name: string;
  imageUrl: string;
  hp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, hp, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader uid={`${uid}-header`}>
        <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <img src={imageUrl} alt={name} className="w-full h-40 object-cover rounded-md" />
      </CardContent>
      <CardFooter uid={`${uid}-footer`}>
        <p>HP: {hp}</p>
      </CardFooter>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
